pip install junit2html
junit2html nose2-junit.xml testrun.html

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
