#!/bin/bash
APPS="paloma foods"
MANAGE="../example/manage.py"
GREP_OPTIONS=
echo  ${APPS}
for M in ${APPS} ; do
    echo ".. digraph:: ${M}" > source/${M}_models.dot ;
    echo ".. digraph:: ${M}" > source/${M}_models_no_members.dot ;
    echo "" >> source/${M}_models.dot ;
    echo "" >> source/${M}_models_no_members.dot ;
    python $MANAGE graph_models ${M}| grep "^ " >> source/${M}_models.dot;
    python $MANAGE graph_models -d ${M}| grep "^ " >> source/${M}_models_no_members.dot;
done
