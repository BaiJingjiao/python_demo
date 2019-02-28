import io.restassured.RestAssured;
import io.restassured.RestAssured.*;
import io.restassured.matcher.RestAssuredMatchers.*;
import io.restassured.specification.RequestSpecification;
import org.hamcrest.Matchers.*;
import io.restassured.module.jsv.JsonSchemaValidator.*;
import io.restassured.module.mockmvc.RestAssuredMockMvc.*;
import io.restassured.response.*;

public class RestTeest {
    public static void main(String[] args) {
        RestAssured.baseURI = "https://10.120.178.239:8443";
        RequestSpecification request = RestAssured.given().relaxedHTTPSValidation();
//        Response response = request.get();
//        Response response = request.relaxedHTTPSValidation().given().auth().basic("xxxxx", "xxxx").when().get("https://10.120.178.239:8443/xxxserver/rest/xxx/xxx/updatexxx");
//        Response response = request.
//                header("Content-Type", "application/json;charset=UTF-8").
//                header("Accept-Language", "zh_CN").
//                header("restUser", "xxxxxxxx").
//                header("passWord", "xxxxxxx").
//                when().post("/xxxserver/rest/xxx/xxx/updatexxx");

        Response response = request.
                header("Content-Type", "application/json").
                header("connection", "Keep-Alive").
                header("accept-encoding", "gzip, deflate").
                header("restUser", "xxxx").
                header("passWord", "xxxxxxsx").
                when().post("/xxxserver/rest/xxx/xxx/updatexxx");
        System.out.println("Status code: " + response.getStatusCode());
        System.out.println("Status message " + response.body().asString());
//        ValidatableResponse response = RestAssured.get(url).then();

    }
}
