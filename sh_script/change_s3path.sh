str='access_key = 5I9JN3DLXXJHFZUIPE5I'

basepath=$(cd `dirname $0`; pwd)
var=`sed -n '2p;' $basepath/.s3cfg`

if [ "$var" == "$str" ]
then
    cp $basepath/train.s3cfg $basepath/.s3cfg
else
    cp $basepath/xcjt.s3cfg $basepath/.s3cfg
fi
