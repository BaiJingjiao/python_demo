<pre>
pip install junit2html
junit2html nose2-junit.xml testrun.html
http://stackoverflow.com/questions/11241781/python-unittests-in-jenkins

https://www.dev2qa.com/python-3-unittest-html-and-xml-report-example/
</pre>

<pre>
[unittest]
plugins = nose2.plugins.mp
          nose2.plugins.junitxml
          nose2.plugins.layers
          nose2.plugins.attrib

[junit-xml]
always-on = True
keep_restricted = False
path = nose2-junit.xml

[multiprocess]
always-on = False
processes = 2
test-run-timeout = 60.0


[layer-reporter]
always-on = True
colors = True
highlight-words = A
                  having
                  should
indent =   

[log-capture]
always-on = True
clear-handlers = true



</pre>
