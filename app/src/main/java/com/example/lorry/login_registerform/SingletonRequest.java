package com.example.lorry.login_registerform;

import android.content.Context;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.Volley;

public class SingletonRequest {

    private static SingletonRequest mInstance;
    private static Context mCtx;
    private RequestQueue requestQueue;

    private SingletonRequest(Context context){
        mCtx = context;
        requestQueue = getRequestQueue();
    }

    private RequestQueue getRequestQueue(){
        if(requestQueue == null){
            requestQueue = Volley.newRequestQueue(mCtx.getApplicationContext());
        }
        return requestQueue;
    }

    public static synchronized SingletonRequest getmInstance(Context context){
        if(mInstance == null){
            mInstance = new SingletonRequest(context);
        }
        return mInstance;
    }

    public<T> void addToRequestQueue(Request<T> request){
        getRequestQueue().add(request);
    }
}
