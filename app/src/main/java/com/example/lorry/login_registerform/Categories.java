package com.example.lorry.login_registerform;

import android.content.Intent;
import android.graphics.Typeface;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.CardView;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;

public class Categories extends AppCompatActivity {

    private CardView[] cards = new CardView[4];
    private TextView[] texts = new TextView[4];
    private String[] cat_names = new String[4];
    private boolean admin;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_categories);

        admin = PreferenceManager.getDefaultSharedPreferences(this).getBoolean("admin", false);
        cards[0] = findViewById(R.id.card_a);
        cards[1] = findViewById(R.id.card_b);
        cards[2] = findViewById(R.id.card_c);
        cards[3] = findViewById(R.id.card_d);
        texts[0] = findViewById(R.id.cat_a);
        texts[1] = findViewById(R.id.cat_b);
        texts[2] = findViewById(R.id.cat_c);
        texts[3] = findViewById(R.id.cat_d);


        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.GET,
                Constants.CATEGORIES_URL,
                null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            if (response.getInt("result") > 0) {
                                JSONArray list = response.getJSONArray("categories");
                                setTexts(list, "name", "n_chal");
                                setListeners(list, "name", "disabled");

                            }
                            else {
                                Toast.makeText(getApplicationContext(), "Something went wrong! Try again later",
                                        Toast.LENGTH_SHORT).show();
                                try{
                                    TimeUnit.SECONDS.sleep(2);
                                    finish();
                                }catch (InterruptedException i){
                                    i.printStackTrace();
                                    finish();
                                }
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }

                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        error.printStackTrace();
                    }
                })
        {

            /**
             * Passing some request headers
             */
            @Override
            public Map<String, String> getHeaders(){
                Map<String, String> headers = new HashMap<>();
                headers.put("Content-Type", "application/json");
                headers.put("authorization", "CIAO");
                return headers;
            }
        };
        SingletonRequest singletonRequest = SingletonRequest.getmInstance(getApplicationContext());
        singletonRequest.addToRequestQueue(jsonObjectRequest);
    }

    private void setTexts(JSONArray json, String key, String nchal){
        try{
            for(int i = 0; i<4; i++){
                JSONObject tmp = json.getJSONObject(i);
                texts[i].setText(getResources().getString(R.string.categories, tmp.getString(key), tmp.getInt(nchal)));
            }
        }catch (JSONException j){
            j.printStackTrace();
        }

    }

    private void setListeners(JSONArray json, String key, String disabled){
        try{
            for(int i = 0; i<4; i++){
                JSONObject tmp = json.getJSONObject(i);
                cat_names[i] = new String(tmp.getString(key));
                if(tmp.getInt(disabled) == 0 && admin == true){
                    final int index = i;
                    cards[i].setOnClickListener(new View.OnClickListener() {
                        @Override
                        public void onClick(View v) {
                            JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.GET,
                                    Constants.GET_CHALLENGE + cat_names[index],
                                    null,
                                    new Response.Listener<JSONObject>() {
                                        @Override
                                        public void onResponse(JSONObject response) {
                                            try {
                                                if (response.getInt("result") > 0) {
                                                    // Saving current_challenge info and current categ
                                                    JSONObject j = new JSONObject();
                                                    j.put("name", cat_names[index]);
                                                    PreferenceManager.getDefaultSharedPreferences(getApplicationContext())
                                                            .edit().putString("current_categ", j.toString()).apply();
                                                    PreferenceManager.getDefaultSharedPreferences(getApplicationContext())
                                                            .edit().putString("current_chal", response.toString()).apply();
                                                    System.out.println(response);
                                                    // Open the challenge activity
                                                    // ........................
                                                }
                                                else {
                                                    // Open the game over activity
                                                    // ...........................
                                                }
                                            } catch (JSONException e) {
                                                e.printStackTrace();
                                            }

                                        }
                                    },
                                    new Response.ErrorListener() {
                                        @Override
                                        public void onErrorResponse(VolleyError error) {
                                            error.printStackTrace();
                                        }
                                    });
                            SingletonRequest singletonRequest = SingletonRequest.getmInstance(getApplicationContext());
                            singletonRequest.addToRequestQueue(jsonObjectRequest);
                        }
                    });
                }
                else{
                    cards[i].setCardBackgroundColor(ContextCompat.getColor(getApplicationContext(), R.color.gray));
                }
            }
        }catch (JSONException j){
            j.printStackTrace();
        }
    }
}
