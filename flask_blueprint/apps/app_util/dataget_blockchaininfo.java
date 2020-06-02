public class main 
    {
        public static void main(String[] args) throws MalformedURLException, IOException
        {
            JSONObject data = getJSONfromURL("https://blockchain.info/charts/market-price?format=json");
            JSONArray data_array = data.getJSONArray("values");

            for (int i = 0; i < data_array.length(); i++)
            {
                JSONObject price_point = data_array.getJSONObject(i);

                //  Unix time
                int x = price_point.getInt("x");

                //  Bitcoin price at that time
                double y = price_point.getDouble("y");

                //  Do something with x and y.
            }

        }

        public static JSONObject getJSONfromURL(String URL)
        {
            try
            {
                URLConnection uc;
                URL url = new URL(URL);
                uc = url.openConnection();
                uc.setConnectTimeout(10000);
                uc.addRequestProperty("User-Agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)");
                uc.connect();

                BufferedReader rd = new BufferedReader(
                        new InputStreamReader(uc.getInputStream(), 
                        Charset.forName("UTF-8")));

                StringBuilder sb = new StringBuilder();
                int cp;
                while ((cp = rd.read()) != -1)
                {
                    sb.append((char)cp);
                }

                String jsonText = (sb.toString());            

                return new JSONObject(jsonText.toString());
            } catch (IOException ex)
            {
                return null;
            }
        }
    }
