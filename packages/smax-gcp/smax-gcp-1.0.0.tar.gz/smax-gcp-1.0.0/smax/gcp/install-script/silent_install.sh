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
    --nfs-host)
    NFS_HOST="$2"
    shift # past argument
    shift # past value
    ;;
    --nfs-shared-name)
    NFS_SHARED_NAME="$2"
    shift # past argument
    shift # past value
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
    --fqdn-ip)
    FQDN_IP="$2"
    shift # past argument
    shift # past value
    ;;
    --registry-org)
    REGISTRY_ORG="$2"
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
filestore_ip=$NFS_HOST
nfs_share_name=$NFS_SHARED_NAME
cdf_admin_password=$CDF_ADMIN_PASSWORD
suite_access_fqdn=$FQDN
suite_access_fqdn_ip=$FQDN_IP
registry_orgname=$REGISTRY_ORG
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

./install --nfs-server ${filestore_ip} \
          --nfs-folder /${nfs_share_name}/var/vols/itom/itsma/core \
          --registry-url gcr.io \
          --registry-username _json_key  \
          --registry-password-file ../registry-key \
          --skip-warning \
          -P ${cdf_admin_password} \
          --external-access-host ${suite_access_fqdn} \
          --cloud-provider gcp \
          --registry-orgname ${registry_orgname} \
          --loadbalancer-info "LOADBALANCERIP=${suite_access_fqdn_ip}" \
          --deployment-name ${suite_ns} \
          -t 120 \
          $silent_install_string $external_cdf_db_string

if [ ! $? -eq 0 ]; then
    echo "cdf installation failed, Please check configuration is correct."
    exit 1
else
    echo "cdf installation finished. Patch ip [${suite_access_fqdn_ip}] for smax BO."
    kubectl patch services itom-nginx-ingress-svc -p '{"spec":{"type":"LoadBalancer", "loadBalancerIP": "${suite_access_fqdn_bound_ip}"}}' -n $(kubectl get namespaces|grep itsma|head -n 1|awk '{print $1}')
fi