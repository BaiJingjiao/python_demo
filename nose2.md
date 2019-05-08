<pre>
pip install junit2html
junit2html nose2-junit.xml testrun.html
http://stackoverflow.com/questions/11241781/python-unittests-in-jenkins

https://www.dev2qa.com/python-3-unittest-html-and-xml-report-example/
</pre>

<pre>
[junit-xml]
always-on = True
keep_restricted = False
path = nose2-junit.xml


[unittest]
plugins = nose2.plugins.mp
          nose2.plugins.junitxml

start-dir = .
test-file-pattern = test*.py
test-method-prefix = test
</pre>
