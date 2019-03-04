package com.eeeeee.emp.resttest;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.security.KeyManagementException;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.UnrecoverableKeyException;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import org.apache.http.HttpHost;
import org.apache.http.StatusLine;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.config.RequestConfig.Builder;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.config.Registry;
import org.apache.http.config.RegistryBuilder;
import org.apache.http.conn.HttpClientConnectionManager;
import org.apache.http.conn.socket.ConnectionSocketFactory;
import org.apache.http.conn.ssl.AllowAllHostnameVerifier;
import org.apache.http.conn.ssl.SSLSocketFactory;
import org.apache.http.conn.ssl.TrustStrategy;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.impl.conn.PoolingHttpClientConnectionManager;

public class eeeeeeClient
{
  private static final String ENCODING = "UTF-8";
  private static final int RET_OK = 200;
  private static final int RET_UNAUTHORIZED = 401;
  private String ip;
  private int port;
  private String userName;
  private String userPswd;
  private String postURI;

  public eeeeeeClient(String ip, int port, String userName, String userPswd, String postURI)
  {
    this.ip = ip;
    this.port = port;
    this.userName = userName;
    this.userPswd = userPswd;
    this.postURI = postURI;
  }

  private HttpClientConnectionManager createSSLConnectionManager()
  {
    HttpClientConnectionManager ccm = null;
    try
    {
      ConnectionSocketFactory sf = new SSLSocketFactory(new TrustStrategyImpl(null), new AllowAllHostnameVerifier());
      Registry r = RegistryBuilder.create()
        .register("https", sf).build();
      ccm = new PoolingHttpClientConnectionManager(r);
    }
    catch (KeyManagementException e)
    {
      e.printStackTrace();
    }
    catch (UnrecoverableKeyException e)
    {
      e.printStackTrace();
    }
    catch (NoSuchAlgorithmException e)
    {
      e.printStackTrace();
    }
    catch (KeyStoreException e)
    {
      e.printStackTrace();
    }
    return ccm;
  }

  public CloseableHttpClient createHttpClient(String inputParams) throws IOException
  {
    HttpHost target = new HttpHost(this.ip, this.port, "https");
    CloseableHttpClient httpclient = HttpClients.custom().setConnectionManager(createSSLConnectionManager())
      .build();

    RequestConfig defaultRequestConfig = RequestConfig.custom()
      .setSocketTimeout(5000)
      .setConnectTimeout(5000)
      .setConnectionRequestTimeout(5000)
      .setStaleConnectionCheckEnabled(true)
      .build();
    try
    {
      HttpPost httpPost = new HttpPost(this.postURI);
      StringEntity entity = new StringEntity(inputParams, "UTF-8");
      httpPost.setEntity(entity);

      CloseableHttpResponse response = httpclient.execute(target, httpPost);
      if (response.getStatusLine().getStatusCode() == 401)
      {
        return auth(inputParams);
      }
    }
    catch (UnsupportedEncodingException e)
    {
      e.printStackTrace();
    }
    catch (ClientProtocolException e)
    {
      e.printStackTrace();
    }

    return httpclient; } 

  private CloseableHttpClient auth(String inputParams) { // Byte code:
 
  public static void main(String[] args) throws IOException { String ip = args[0];
    String password = args[1];
    String appId = "eeeeee" + ip; String postURI = "/open/appAuth.action";
    int port = 18443;
    String testStr = "<message><head><appid>" + appId + "</appid><pwd>" + password + "</pwd></head></message>";
    new eeeeeeClient(ip, port, appId, password, postURI).createHttpClient(testStr);
  }

  private static class TrustStrategyImpl
    implements TrustStrategy
  {
    public boolean isTrusted(X509Certificate[] chain, String authType)
      throws CertificateException
    {
      return true;
    }
  }
}
