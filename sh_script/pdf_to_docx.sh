sh_script=$(cd `dirname $0`; pwd)
dependence=$sh_script"/dependence"
cd $dependence

pdf_path="$1"
python pdf_to_docx.py $pdf_path
