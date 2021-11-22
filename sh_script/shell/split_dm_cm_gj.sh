

all_path=$1
split_path=$2

mkdir -p $split_path/dm $split_path/cm $split_path/gj

cd $all_path
cp `ls | egrep '*13.jpg|*14.jpg|*15.jpg|*16.jpg|*13.json|*14.json|*15.json|*16.json'` $split_path/dm/

cp `ls | egrep '*05.jpg|*06.jpg|*07.jpg|*08.jpg|*09.jpg|*10.jpg|*11.jpg|*12.jpg|*05.json|*06.json|*07.json|*08.json|*09.json|*10.json|*11.json|*12.json'` $split_path/cm/

cp `ls | egrep '*01.jpg|*02.jpg|*03.jpg|*04.jpg|*01.json|*02.json|*03.json|*04.json'` $split_path/gj/
