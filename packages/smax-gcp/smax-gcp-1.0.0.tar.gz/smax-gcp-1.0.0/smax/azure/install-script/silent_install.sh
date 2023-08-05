#!/bin/bash
POSITIONAL=()
while [[ $# -gt 0 ]]; do
key="$1"
case $key in
    -c|--cdf-package)
    CDF_PACKAGE="$2"
    shift # past argument
    shift # past value
    ;;
    -s|--suite-package)
    SUITE_METADATA_PACKAGE="$2"
    shift # past argument
    shift # past value
    ;;
    --db-host)
    DB_HOST="$2"
    shift # past argument
    shift # past value
    ;;
    --cdf-api-db-password)
    CDF_DB_PASSWORD="$2"
    shift # past argument
    shift # past value
    ;;
    --cdf-api-db)
    CDF_API_DB="$2"
    shift # past argument
    shift # past value
    ;;
    --cdf-api-db-user)
    CDF_API_DB_USER="$2"
    shift # past argument
    shift # past value
    ;;
    --use-external-db)
    USE_EXTERNAL_DB="$2"
    shift # past argument with no value
    ;;
    --cdf-admin-password)
    CDF_ADMIN_PASSWORD="$2"
    shift # past argument
    shift # past value
    ;;
    --fqdn)
    FQDN="$2"
    shift # past argument
    shift # past value
    ;;
    --registry-org)
    REGISTRY_ORG="$2"
    shift # past argument
    shift # past value
    ;;
    --registry-url)
    REGISTRY_URL="$2"
    shift # past argument
    shift # past value
    ;;
    --registry-pwd)
    REGISTRY_PWD="$2"
    shift # past argument
    shift # past value
    ;;
    --registry-user)
    REGISTRY_USER="$2"
    shift # past argument
    shift # past value
    ;;
    --suite-ns)
    SUITE_NS="$2"
    shift # past argument
    shift # past value
    ;;
    *) # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

deployerZipFile=$CDF_PACKAGE
deployerName="${deployerZipFile%.*}"
metaDataFile=$SUITE_METADATA_PACKAGE
use_external_db=$USE_EXTERNAL_DB
cdfapi_db_ip=$DB_HOST
cdfapi_db=$CDF_API_DB
cdfapi_db_user=$CDF_API_DB_USER
cdfapi_db_password=$CDF_DB_PASSWORD
configFile="config.json"
cdf_admin_password=$CDF_ADMIN_PASSWORD
suite_access_fqdn=$FQDN
reg_org=$REGISTRY_ORG
reg_url=$REGISTRY_URL
reg_username=$REGISTRY_USER
reg_password=$REGISTRY_PWD
suite_ns=$SUITE_NS

TIMEOUT_FOR_SERVICES=120
n=0
while :; do
    n=$(($n + 1))
	if [[ $n -ge $TIMEOUT_FOR_SERVICES ]]; then
		echo "check nodes ready timeout."
        exit 1
	fi
    readyNode=`kubectl get nodes| grep Ready |wc -l`
    if [[ $readyNode -ge 1 ]];  then
		echo "There are one or more worker nodes ready for schedule pods!"
		break
	fi
	sleep 15
done

unzip -oq ./$deployerZipFile
cd $deployerName
chmod -R 755 *

silent_install_string=" --metadata ../$metaDataFile --config ../$configFile"

external_cdf_db_string=""
if [ "$use_external_db" = "True" ]; then
    external_cdf_db_string=" --db-user ${cdfapi_db_user} \
    --db-password ${cdfapi_db_password} \
    --db-url jdbc:postgresql://${cdfapi_db_ip}:5432/${cdfapi_db} "
fi


./install --registry-url ${reg_url} \
          --registry-username ${reg_username} \
          --registry-password ${reg_password} \
          --skip-warning \
          -P ${cdf_admin_password} \
          --external-access-host ${suite_access_fqdn} \
          --cloud-provider AZURE \
          --registry-orgname ${reg_org} \
          --deployment-name ${suite_ns} \
          -t 120 \
          $silent_install_string $external_cdf_db_string

if [ ! $? -eq 0 ]; then
    echo "cdf installation failed, Please check configuration is correct."
    exit 1
fi

kubectl patch services itom-nginx-ingress-svc -p '{"metadata":{"annotations":{"service.beta.kubernetes.io/azure-load-balancer-internal": "true"}},"spec":{"type":"LoadBalancer"}}' -n $(kubectl get namespaces|grep itsma|head -n 1|awk '{print $1}')
sleep 1
kubectl patch services itom-cdf-ingress-frontend-svc -p '{"metadata":{"annotations":{"service.beta.kubernetes.io/azure-load-balancer-internal": "true"}},"spec":{"type":"LoadBalancer"}}' -n core
sleep 1
kubectl patch services nginx-ingress-controller-svc -p '{"metadata":{"annotations":{"service.beta.kubernetes.io/azure-load-balancer-internal": "true"}},"spec":{"type":"LoadBalancer"}}' -n core

sleep 15
n=0
while :; do
    n=$(($n + 1))
    if [[ $n -ge $TIMEOUT_FOR_SERVICES ]]; then
        echo "check loadbalancer ip ready timeout."
        exit 1
    fi
    externalip_443=$(kubectl get svc itom-nginx-ingress-svc -n $(kubectl get namespaces | grep itsma | head -n 1 | awk '{print $1}') | grep -v EXTERNAL-IP | awk '{print $4}')
    externalip_5443=$(kubectl get svc nginx-ingress-controller-svc -n core | grep -v EXTERNAL-IP |awk '{print $4}')
    externalip_3000=$(kubectl get svc itom-cdf-ingress-frontend-svc -n core | grep -v EXTERNAL-IP | awk '{print $4}')
    if [ $externalip_443 != "<none>" ] && [ $externalip_443 != "<pending>" ] && [ $externalip_5443 != "<none>" ] && \
    [ $externalip_5443 != "<pending>" ] && [ $externalip_3000 != "<none>" ] && [ $externalip_3000 != "<pending>" ]; then
        echo "Loadbalancers are ready, the external public ips are :$externalip_443, $externalip_5443, $externalip_3000"
        break
    fi
    sleep 10
done