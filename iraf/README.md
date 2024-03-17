# Things to do to feather the nest
# a few file positions need to be deduced.

export IRAF='/wherever/iraf/is/installed'

Review and run the feather.bash script.


#Aliases
function fixnames  {
                    (for f in *; do if [[ "$f" =~ " " ]] ; then mv "$f" ${f// /_} ; fi ; done)
                    (shopt -s nullglob; for f in *.*.*fit    ; do mv  $f  ${f//./_}        ; done)
                     (shopt -s nullglob; for f in *-*fit      ; do mv  $f  ${f//-/m}        ; done)
                    (shopt -s nullglob; for f in *+*fit      ; do mv  $f  ${f//+/p}        ; done)
                     (shopt -s nullglob; for f in *_fit       ; do mv  $f  ${f/%_fit/.fits} ; done)
                    (shopt -s nullglob; for f in *.fit       ; do mv  $f  ${f/%.fit/.fits} ; done)
                     (shopt -s nullglob; for f in *           ; do if test -f $f ; then chmod -x $f; fi; done)
                   }

                   
