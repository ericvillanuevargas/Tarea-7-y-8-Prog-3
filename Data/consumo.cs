using Newtonsoft.Json;
using RestSharp;
using System;
using System.IO;
using System.Net;
using System.Web;
class consumo {
    public dynamic Post(string url, string json, string autorizacion = null)
            {
                try
                {
                    var client = new RestClient(url);
                    var request = new RestRequest(Method.POST);
                    request.AddHeader("content-type", "application/json");
                    request.AddParameter("application/json", json, ParameterType.RequestBody);
                    if (autorizacion != null)
                    {
                        request.AddHeader("Authorization", autorizacion);
                    }
                    IRestResponse response = client.Execute(request);
                    dynamic datos = JsonConvert.DeserializeObject(response.Content);
                    return datos;
                }
                catch (Exception )
                {
                    return null;
                }
            }
            public dynamic Get(string url)
            {
                try
                {
                    HttpWebRequest myWebRequest = (HttpWebRequest)WebRequest.Create(url);
                    myWebRequest.UserAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0";
                    myWebRequest.Credentials = CredentialCache.DefaultCredentials;
                    myWebRequest.Proxy = null;
                    HttpWebResponse myHttpWebResponse = (HttpWebResponse)myWebRequest.GetResponse();
                    Stream myStream = myHttpWebResponse.GetResponseStream();
                    StreamReader myStreamReader = new StreamReader(myStream);
                   
                    string Datos = HttpUtility.HtmlDecode(myStreamReader.ReadToEnd());
                    dynamic data = JsonConvert.DeserializeObject(Datos);
                    return data;
                }
                catch (Exception)
                {
                    Console.Write("Lo sentimos, Ocurrio un error...");
                    return false;
                }
            }
}