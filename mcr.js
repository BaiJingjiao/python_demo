jQuery(document).ready(function() {
    jQuery('.tabs .tab-links a').on('click', function(e)  {
        var currentAttrValue = jQuery(this).attr('href');
 
        // Show/Hide Tabs
        jQuery('.tabs ' + currentAttrValue).show().siblings().hide();
 
        // Change/remove current tab to active
        jQuery(this).parent('li').addClass('active').siblings().removeClass('active');
 
        e.preventDefault();
    });
});

function setIframeHeight(id) { 
    var ifrm = document.getElementById(id); 
    var doc = ifrm.contentDocument? ifrm.contentDocument:  
        ifrm.contentWindow.document; 
    ifrm.style.visibility = 'hidden'; 
    ifrm.style.height = "10px"; // reset to minimal height ... 
    ifrm.style.height = getDocHeight( doc ) + 4 + "px"; 
    ifrm.style.visibility = 'visible'; 
} 
 
function getDocHeight(doc) { 
    doc = doc || document; 
    var body = doc.body, html = doc.documentElement; 
    var height = Math.max( body.scrollHeight, body.offsetHeight,  
        html.clientHeight, html.scrollHeight, html.offsetHeight ); 
    return height; 
} 
