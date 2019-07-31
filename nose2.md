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

```
<html>  
<head>  
    <meta charset="UTF-8" />  
    <title>HTML5 Demo</title>  
</head>  
<body>  
    <canvas id="circle" width="400" height="300">您的浏览器暂不支持Canvas</canvas>  
            <script type="text/javascript">  
            var color = ["#27255F","#2F368F","#3666B0","#2CA8E0","#77D1F6"];  
            var data = [5,30,15,30,20];  
              
            function drawCircle(){  
                var canvas = document.getElementById("circle");  
                var ctx = canvas.getContext("2d");  
                var startPoint = 1.5 * Math.PI;  
                for(var i=0;i<data.length;i++){  
                    ctx.fillStyle = color[i];  
                    ctx.strokeStyle = color[i];  
                    ctx.beginPath();  
                    ctx.moveTo(200,150);  
                    ctx.arc(200,150,150,startPoint,startPoint-Math.PI*2*(data[i]/100),true);  
                    ctx.fill();  
                    ctx.stroke();  
                    startPoint -= Math.PI*2*(data[i]/100);  
                }  
            }  
            drawCircle();  
            </script> 
</body> 

</html>

```
