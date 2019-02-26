package utils;

import java.io.Serializable;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.openqa.selenium.*;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.internal.FindsByClassName;
import org.openqa.selenium.internal.FindsByCssSelector;
import org.openqa.selenium.internal.FindsById;
import org.openqa.selenium.internal.FindsByLinkText;
import org.openqa.selenium.internal.FindsByName;
import org.openqa.selenium.internal.FindsByTagName;
import org.openqa.selenium.internal.FindsByXPath;
import org.openqa.selenium.support.ui.*;
import utils.drivers.DriverManager;


/**
 * Provide basic methods for WebElement identification, 
 * basic operations on WebElement level, and basic driver.
 * @author baijingjiao
 *
 */
public class BaseUtil extends By {
	
	private WebDriver driver;
	
	private int WAITTIME_FOR_ELEMENT = 20; // seconds
	private int WAITTIME_FOR_AJAX = 20; // seconds

	public static void sleep(long millis) {
		try {
			Thread.sleep(millis);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	public BaseUtil() {
		this.driver = DriverManager.getDriver();
		if(!isJQueryInThisPage()) {
			injectJQuery();
		}
	}
	
	private String getAjaxStatus() {
		String jsStr = "return window.custom_named_status;";
		String ajax = (String) ((JavascriptExecutor) getDriver() ).executeScript(jsStr);
		return ajax;
	}
	
	private void injectAjaxObserver() {
		String jsStr = "var headID_my=document.getElementsByTagName(\"head\")[0];" +
				"var newScript_my = document.createElement('script');" +
				"newScript_my.type='text/javascript';" +
				"newScript_my.src='https://coding.net/u/baijingjiao/p/sharedocs/git/raw/master/ajax.observer.js';" +
				"headID_my.appendChild(newScript_my);";
		((JavascriptExecutor) getDriver() ).executeScript(jsStr);
//		System.out.println("Ajax Observer injected!");
	}
	
	private  boolean isJQueryInThisPage() {
	    Boolean loaded;
	    try {
	        loaded = (Boolean) ((JavascriptExecutor) getDriver() ).executeScript("return jQuery()!=null");
	    } catch (Exception e) {
	        loaded = false;
	    }
	    return loaded;
	}
	
	public void executeJs(String jsStr) {
		sleep(500);
		System.out.println(jsStr);
		((JavascriptExecutor)getDriver()).executeScript(jsStr);
		sleep(500);
	}

	private void injectJQuery() {
	    String jsStr = "var headID=document.getElementsByTagName(\"head\")[0];" +
	                    "var newScript = document.createElement('script');" +
	                    "newScript.type='text/javascript';" +
	                    "newScript.src='//ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js';" +
	                    "headID.appendChild(newScript);";
	    ((JavascriptExecutor) getDriver() ).executeScript(jsStr);
//	    System.out.println("Jquery injected.");
	}
	
	public WebDriver getDriver() {
		return this.driver;
	}
	
	public void setDriver(WebDriver driver) {
		this.driver = driver;
	}
	
	public String getCurrentUrl() {
		return getDriver().getCurrentUrl();
	}
	
	public String getPageSource() {
		return this.getDriver().getPageSource();
	}
	
    public void savePageSourceToFile(String filename) {
        String path = System.getProperty("user.dir")
                + System.getProperty("file.separator")
                + "temp"
                + System.getProperty("file.separator");
        String tempFile = path + filename + Helper.getSystemDateTime("yyyy-MM-dd-HH-mm-ss-SSS-z");
        
        String source = this.driver.getPageSource();
        Helper.writeToFileAppendMode(tempFile, source);
        Helper.printStr("Saved page source to file: " + tempFile);
    }
	
	public void get(String url) {
		getDriver().get(url);
	}
	
	public void refresh() {
		getDriver().navigate().refresh();
	}
	
    @SuppressWarnings("unchecked")
	public List<String> jsExecutor(String jsStr) {
    	return (List<String>)((JavascriptExecutor)getDriver()).executeScript(jsStr);
    }

	/**
	 * 关于ExpectedConditions的问题：https://github.com/SeleniumHQ/selenium/issues/3606
	 * 关于找不到Selenium 3.x 的官方文档：https://groups.google.com/forum/#!topic/selenium-users/v3PmIhBvt9w
	 * 别人的解决方案：https://stackoverflow.com/questions/44877479/selenium-3-4-how-to-use-changed-wait-until
	 * 别人的解决方案：https://stackoverflow.com/questions/31102351/selenium-java-lambda-implementation-for-explicit-waits/31102550
	 */
	public void waitElementReady() {
		injectAjaxObserver();
		String ajax = getAjaxStatus();
//		System.out.println("ajax: " + ajax);
		WebDriverWait wait = new WebDriverWait(driver, WAITTIME_FOR_ELEMENT); 
//      wait.until(ExpectedConditions.visibilityOf(findElement()));
//		wait.until(ExpectedConditions.visibilityOfElementLocated(this));
		wait.until((WebDriver dr) -> dr.findElement(this));
	}
	
	public void waitElementClickable() {
		waitElementReady();
		WebDriverWait wait = new WebDriverWait(driver, WAITTIME_FOR_ELEMENT); 
//        wait.until(ExpectedConditions.elementToBeClickable(findElement()));
		wait.until((WebDriver dr) -> dr.findElement(this));
		sleep(200);
	}
	
	public void waitAjaxComplete() {
		String script = "return typeof $ === 'function' && $.active === 0 && document.readyState === 'complete'";
		for(int i=0;i<WAITTIME_FOR_AJAX*5;i++) {
			boolean flag = (Boolean)((JavascriptExecutor)driver).executeScript(script);
			if(flag==true) {
				break;
			} else {
				sleep(200);
			}
		}
	}
	
	public WebElement findElement() {
		WebElement ele = getDriver().findElement(this);
//		scrollTo(0, 0);
		scrollIntoView(ele);
		return ele;
	}
	
	public List<WebElement> findElements(By by) {
		return driver.findElements(by);
	}
	
	public Boolean isDisplayed() {
		try {
			Thread.sleep(500);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		if (findElements().size()==0) {
			return false;
		} else {
			return findElement().isDisplayed();
		}
	}
	
	public Boolean isSelected() {
		try {
			Thread.sleep(500);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		if (findElements().size()==0) {
			return false;
		} else {
			return findElement().isSelected();
		}
	}
	
	private void scrollTo(int x, int y) {
		((JavascriptExecutor) driver).executeScript("window.scrollBy("+x+", "+y+");");
	}
	
	public void scrollToPageBottom() {
		String jsStr = "window.scrollTo(0,document.body.scrollHeight)";
		((JavascriptExecutor) driver).executeScript(jsStr);
	}
	
	private void scrollIntoView(WebElement element) {
		int y = element.getLocation().getY(); 
        Dimension dimension = driver.manage().window().getSize();
        int maxy = dimension.getHeight();
        ((JavascriptExecutor) driver).executeScript("window.scrollBy(0, "+(-y-maxy*5)+");");
//        ((JavascriptExecutor) getDriver()).executeScript("$(document).scrollTop(0);");
        if (y >= dimension.getHeight()-300) {
            ((JavascriptExecutor) driver).executeScript("window.scrollBy(0, "+(y-maxy/2)+");");
        }
	}
	
	public void click() {
		waitElementClickable();
		sleep(500);
		WebElement element = findElement();
		element.click();
//		Actions action = new Actions(driver);
//		action.moveToElement(element).click().perform();

	}
	
	public void input(Keys key) {
		Actions action = new Actions(driver);
		action.sendKeys(Keys.PAGE_DOWN).build().perform();
	}

	public void input(String text) {
		waitElementReady();
		WebElement e = findElement();
		try {
			e.clear();
			e.sendKeys(text);
		} catch (Exception ex) {
//			ex.printStackTrace();
			inputValUsingJQuery(text);
		}
		try {
			blur();
		} catch (Exception ex) {
			
		}
	}
	
	public void input_specialClear(String text) {
		waitElementReady();
		Actions action = new Actions(driver);
		WebElement e = findElement();
		int lenText = e.getAttribute("value").length();

		e.click();
		for(int i = 0; i < lenText; i++){
		  action.sendKeys(Keys.ARROW_LEFT);
		}
		action.build().perform();

		for(int i = 0; i < lenText; i++){
		  action.sendKeys(Keys.DELETE);
		}
//		WaitTool.sleep(200);
		action.build().perform();
		e.sendKeys(text);
		try {
			blur();
		} catch (Exception ex) {
			
		}
	}
	
	public void clear() {
		Actions action = new Actions(driver);
		WebElement e = findElement();
		int lenText = e.getAttribute("value").length();

		for(int i = 0; i < lenText; i++){
		  action.sendKeys(Keys.ARROW_LEFT);
		}
		action.build().perform();

		for(int i = 0; i < lenText; i++){
		  action.sendKeys(Keys.DELETE);
		}
		sleep(1000);
		action.build().perform();
	}
	
	public void check() {
		waitElementReady();
		WebElement e = findElement();
		if(!e.isSelected()) {
			e.click();
		}
	}
	
	public void uncheck() {
		waitElementReady();
		WebElement e = findElement();
		if(e.isSelected()) {
			e.click();
		}
	}
	
	public void inputValUsingJQuery(String text) {
		String id = this.getAttribute("id");
		String name = this.getAttribute("name");
		String jsStr = "";
		if (id!=null && id.length()!=0) {
			jsStr = "$(\"#" + id + "\").val(\"" + text + "\");";
		} else if (name!=null && name.length()!=0) {
			jsStr = "$(\"#" + name + "\").val(\"" + text + "\");";
		}
		((JavascriptExecutor)driver).executeScript(jsStr);
		change();
		blur();
	}
	
	public void clearUsingJQuery() {
		String id = this.getAttribute("id");
		String name = this.getAttribute("name");
		String jsStr = "";
		if (id!=null && id.length()!=0) {
			jsStr = "$(\"#" + id + "\").val(\""+"\");";
		} else if (name!=null && name.length()!=0) {
			jsStr = "$(\"#" + name + "\").val(\""+"\");";
		}
		((JavascriptExecutor)driver).executeScript(jsStr);
	}
	
	public void blur() {
		String id = this.getAttribute("id");
		String name = this.getAttribute("name");
		String jsStr = "";
		if (id!=null && id.length()!=0) {
			jsStr = "$(\"#" + id + "\").blur();";
		} else if (name!=null && name.length()!=0) {
			jsStr = "$(\"#" + name + "\").blur();";
		}
		((JavascriptExecutor)driver).executeScript(jsStr);
	}
	
	public void change() {
		String id = this.getAttribute("id");
		String name = this.getAttribute("name");
		String jsStr = "";
		if (id!=null && id.length()!=0) {
			jsStr = "$(\"#" + id + "\").change();";
		} else if (name!=null && name.length()!=0) {
			jsStr = "$(\"#" + name + "\").change();";
		}
		((JavascriptExecutor)driver).executeScript(jsStr);
	}
	
	public Select getSelect() {
		waitElementReady();
		WebElement e = findElement();
		blur();
		Select s = new Select(e);
		return s;
	}
	
	public void dragFrom(By fromBy) {
		Actions action = new Actions(getDriver());
		WebElement fromEle = findElement();
		WebElement toEle = findElement();
		action.dragAndDrop(fromEle, toEle).build().perform();;
	}

	public void dragTo(By toBy) {
		Actions action = new Actions(getDriver());
		WebElement fromEle = findElement();
		WebElement toEle = findElement();
		action.dragAndDrop(fromEle, toEle).build().perform();
	}

	public void moveMouseOn() {
		Actions action = new Actions(driver);
		action.moveToElement(findElement()).build().perform();
		sleep(500);
	}
	
	public void doubleClick() {
		Actions action = new Actions(driver);
		action.doubleClick(this.findElement()).build().perform();;
	}
	
	public String getAttribute(String attr){
		return findElement().getAttribute(attr);
	}
	
	public String getText() {
		return findElement().getText();
	}
	
	public void acceptAlert() {
		sleep(1000);
		driver.switchTo().alert().accept();
	}
	
	public String getAlertContent() {
		sleep(1000);
		return driver.switchTo().alert().getText();
	}
	
	public void switchToThisFrame() {
		sleep(1000);
		driver.switchTo().frame(findElement());
	}
	
	public void switchToDefaultContent() {
		driver.switchTo().defaultContent();
	}
	
	/**
	 * Please do not use this method. You can use {@link #findElement()}.
	 */
	@Deprecated
	@Override
	public List<WebElement> findElements(SearchContext arg0) {
		// TODO Auto-generated method stub
		return null;
	}
	
	/**
	 * @param id The value of the "id" attribute to search for
	 * @return a By which locates elements by the value of the "id" attribute.
	 */
	public static BaseUtil id(final String id) {
		if (id == null)
			throw new IllegalArgumentException(
												"Cannot find elements with a null id attribute.");

		return new ById(id);
	}

	/**
	 * @param linkText The exact text to match against
	 * @return a By which locates A elements by the exact text it displays
	 */
	public static BaseUtil linkText(final String linkText) {
		if (linkText == null)
			throw new IllegalArgumentException(
												"Cannot find elements when link text is null.");

		return new ByLinkText(linkText);
	}

	/**
	 * @param linkText The text to match against
	 * @return a By which locates A elements that contain the given link text
	 */
	public static BaseUtil partialLinkText(final String linkText) {
		if (linkText == null)
			throw new IllegalArgumentException(
												"Cannot find elements when link text is null.");

		return new ByPartialLinkText(linkText);
	}

	/**
	 * @param name The value of the "name" attribute to search for
	 * @return a By which locates elements by the value of the "name" attribute.
	 */
	public static BaseUtil name(final String name) {
		if (name == null)
			throw new IllegalArgumentException(
												"Cannot find elements when name text is null.");

		return new ByName(name);
	}

	/**
	 * @param name The element's tagName
	 * @return a By which locates elements by their tag name
	 */
	public static BaseUtil tagName(final String name) {
		if (name == null)
			throw new IllegalArgumentException(
												"Cannot find elements when name tag name is null.");

		return new ByTagName(name);
	}
	
	/**
	 * @param xpathExpression The xpath to use
	 * @return a By which locates elements via XPath
	 */
	public static BaseUtil xpath(final String xpathExpression) {
		if (xpathExpression == null)
			throw new IllegalArgumentException(
												"Cannot find elements when the XPath expression is null.");
//		System.out.println(xpathExpression);
		return new ByXPath(xpathExpression);
	}
	
	private static final String VAR_PATTERN = "(#\\{Var\\(\\d+\\)\\}#)";
	
	/**
	 * @param xpathExpression The xpath to use
	 * @return a By which locates elements via XPath
	 */
	public static BaseUtil xpath(final String xpathExpression, String...variables) {
		if (xpathExpression == null)
			throw new IllegalArgumentException(
												"Cannot find elements when the XPath expression is null.");
		Pattern p = Pattern.compile(VAR_PATTERN);
		Matcher m = p.matcher(xpathExpression);
		if(variables!=null&&variables.length!=0){
			if(m.groupCount()!=variables.length){
				throw new IllegalArgumentException(
						"The xpath ["+xpathExpression+"] parameters' number("+m.groupCount()+") should be equle to the variables' number("+variables.length+")");
			}else{
				for(String var : variables){
					while(m.find()){
						xpathExpression.replace(m.group(), var);
					}
				}
			}
		}
		return new ByXPath(xpathExpression);
	}

	/**
	 * Finds elements based on the value of the "class" attribute. If an element has many classes then this will match
	 * against each of them. For example if the value is "one two onone", then the following "className"s will match:
	 * "one" and "two"
	 * 
	 * @param className The value of the "class" attribute to search for
	 * @return a By which locates elements by the value of the "class" attribute.
	 */
	public static BaseUtil className(final String className) {
		if (className == null)
			throw new IllegalArgumentException(
												"Cannot find elements when the class name expression is null.");

		return new ByClassName(className);
	}

	/**
	 * Finds elements via the driver's underlying W3 Selector engine. If the browser does not implement the Selector
	 * API, a best effort is made to emulate the API. In this case, we strive for at least CSS2 support, but offer no
	 * guarantees.
	 */
	public static BaseUtil cssSelector(final String selector) {
		if (selector == null)
			throw new IllegalArgumentException(
												"Cannot find elements when the selector is null");

		return new ByCssSelector(selector);

	}

	/**
	 * Please do not use this method. You can use {@link #findElement()}.
	 */
	@Deprecated
	public WebElement findElement(SearchContext context) {
		return getDriver().findElement(this);
	}

	public List<WebElement> findElements() {
		return getDriver().findElements(this);
	}

	@Override
	public boolean equals(Object o) {
		if (this == o)
			return true;
		if (o == null || getClass() != o.getClass())
			return false;

		By by = (By) o;

		return toString().equals(by.toString());
	}

	@Override
	public int hashCode() {
		return toString().hashCode();
	}

	@Override
	public String toString() {
		// A stub to prevent endless recursion in hashCode()
		return "[unknown locator]";
	}

	private static class ById extends BaseUtil implements Serializable {

		private static final long serialVersionUID = 5341968046120372169L;

		private final String id;

		public ById(String id) {
			this.id = id;
		}

		@Override
		public List<WebElement> findElements(SearchContext context) {
			if (context instanceof FindsById)
				return ((FindsById) context).findElementsById(id);
			return ((FindsByXPath) context).findElementsByXPath(".//*[@id = '"
																+ id
																+ "']");
		}

		@Override
		public WebElement findElement(SearchContext context) {
			if (context instanceof FindsById)
				return ((FindsById) context).findElementById(id);
			return ((FindsByXPath) context).findElementByXPath(".//*[@id = '"
																+ id
																+ "']");
		}

		@Override
		public String toString() {
			return "By.id: " + id;
		}
	}

	private static class ByLinkText extends BaseUtil implements Serializable {

		private static final long serialVersionUID = 1967414585359739708L;

		private final String linkText;

		public ByLinkText(String linkText) {
			this.linkText = linkText;
		}

		@Override
		public List<WebElement> findElements(SearchContext context) {
			return ((FindsByLinkText) context).findElementsByLinkText(linkText);
		}

		@Override
		public WebElement findElement(SearchContext context) {
			return ((FindsByLinkText) context).findElementByLinkText(linkText);
		}

		@Override
		public String toString() {
			return "By.linkText: " + linkText;
		}
	}

	private static class ByPartialLinkText extends BaseUtil implements
															Serializable {

		private static final long serialVersionUID = 1163955344140679054L;

		private final String linkText;

		public ByPartialLinkText(String linkText) {
			this.linkText = linkText;
		}

		@Override
		public List<WebElement> findElements(SearchContext context) {
			return ((FindsByLinkText) context)
												.findElementsByPartialLinkText(linkText);
		}

		@Override
		public WebElement findElement(SearchContext context) {
			return ((FindsByLinkText) context).findElementByPartialLinkText(linkText);
		}

		@Override
		public String toString() {
			return "By.partialLinkText: " + linkText;
		}
	}

	private static class ByName extends BaseUtil implements Serializable {

		private static final long serialVersionUID = 376317282960469555L;

		private final String name;

		public ByName(String name) {
			this.name = name;
		}

		@Override
		public List<WebElement> findElements(SearchContext context) {
			if (context instanceof FindsByName)
				return ((FindsByName) context).findElementsByName(name);
			return ((FindsByXPath) context).findElementsByXPath(".//*[@name = '"
																+ name + "']");
		}

		@Override
		public WebElement findElement(SearchContext context) {
			if (context instanceof FindsByName)
				return ((FindsByName) context).findElementByName(name);
			return ((FindsByXPath) context).findElementByXPath(".//*[@name = '"
																+ name + "']");
		}

		@Override
		public String toString() {
			return "By.name: " + name;
		}
	}

	private static class ByTagName extends BaseUtil implements Serializable {

		private static final long serialVersionUID = 4699295846984948351L;

		private final String name;

		public ByTagName(String name) {
			this.name = name;
		}

		@Override
		public List<WebElement> findElements(SearchContext context) {
			if (context instanceof FindsByTagName)
				return ((FindsByTagName) context).findElementsByTagName(name);
			return ((FindsByXPath) context).findElementsByXPath(".//" + name);
		}

		@Override
		public WebElement findElement(SearchContext context) {
			if (context instanceof FindsByTagName)
				return ((FindsByTagName) context).findElementByTagName(name);
			return ((FindsByXPath) context).findElementByXPath(".//" + name);
		}

		@Override
		public String toString() {
			return "By.tagName: " + name;
		}
	}

	protected static class ByXPath extends BaseUtil implements Serializable {

		private static final long serialVersionUID = -6727228887685051584L;

		private final String xpathExpression;

		public ByXPath(String xpathExpression) {
			this.xpathExpression = xpathExpression;
		}

		@Override
		public List<WebElement> findElements(SearchContext context) {
			return ((FindsByXPath) context).findElementsByXPath(xpathExpression);
		}

		@Override
		public WebElement findElement(SearchContext context) {
			return ((FindsByXPath) context).findElementByXPath(xpathExpression);
		}

		@Override
		public String toString() {
			return "By.xpath: " + xpathExpression;
		}
		
		public String getXpath(){
			return xpathExpression;
		}
	}

	private static class ByClassName extends BaseUtil implements Serializable {

		private static final long serialVersionUID = -8737882849130394673L;

		private final String className;

		public ByClassName(String className) {
			this.className = className;
		}

		@Override
		public List<WebElement> findElements(SearchContext context) {
			if (context instanceof FindsByClassName)
				return ((FindsByClassName) context).findElementsByClassName(className);
			return ((FindsByXPath) context).findElementsByXPath(".//*["
																+ containingWord(	"class",
																					className)
																+ "]");
		}

		@Override
		public WebElement findElement(SearchContext context) {
			if (context instanceof FindsByClassName)
				return ((FindsByClassName) context).findElementByClassName(className);
			return ((FindsByXPath) context).findElementByXPath(".//*["
																+ containingWord(	"class",
																					className)
																+ "]");
		}

		/**
		 * Generates a partial xpath expression that matches an element whose specified attribute contains the given CSS
		 * word. So to match &lt;div class='foo bar'&gt; you would say "//div[" + containingWord("class", "foo") + "]".
		 * 
		 * @param attribute name
		 * @param word name
		 * @return XPath fragment
		 */
		private String containingWord(String attribute, String word) {
			return "contains(concat(' ',normalize-space(@" + attribute
					+ "),' '),' "
					+ word + " ')";
		}

		@Override
		public String toString() {
			return "By.className: " + className;
		}
	}

	private static class ByCssSelector extends BaseUtil implements Serializable {

		private static final long serialVersionUID = -3910258723099459239L;

		private final String selector;

		public ByCssSelector(String selector) {
			this.selector = selector;
		}

		@Override
		public WebElement findElement(SearchContext context) {
			if (context instanceof FindsByCssSelector) {
				return ((FindsByCssSelector) context)
														.findElementByCssSelector(selector);
			}

			throw new WebDriverException(
											"Driver does not support finding an element by selector: "
													+ selector);
		}

		@Override
		public List<WebElement> findElements(SearchContext context) {
			if (context instanceof FindsByCssSelector) {
				return ((FindsByCssSelector) context)
														.findElementsByCssSelector(selector);
			}

			throw new WebDriverException(
											"Driver does not support finding elements by selector: "
													+ selector);
		}

		@Override
		public String toString() {
			return "By.cssSelector: " + selector;
		}
	}
}
