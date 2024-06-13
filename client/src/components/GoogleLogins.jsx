import React from "react";
// import { GoogleLogin } from "@react-oauth/google";
import { GoogleOAuthProvider, useGoogleLogin } from "@react-oauth/google";

function GoogleLogIns() {
  const login = useGoogleLogin({
    onSuccess: async (response) => {
      const { access_token } = response;
      try {
        const res = await fetch(
          "https://127.0.0.1:5555/login/authorized",
          {
            method: "GET",
          },
          access_token
        );
        const { data } = res;
        const { access_token: backendAccessToken, refresh_token } = data;
        localStorage.setItem("access", backendAccessToken);
        localStorage.setItem("refresh", refresh_token);
      } catch (error) {
        console.error("An expected erroor occured", error);
      }
    },
  });
  return (
    <div className="block w-full mt-4 relative p-4">
      <button
        onClick={() => login()}
        className=" py-3 flex justify-center w-96 text-center text-stone-900 border border-gray-700 rounded-md"
      >
        <FcGoogle fontSize={"1.3rem"} />
        Sign with Google
      </button>
    </div>
  );
}

  const GoogleAuthProviderWrapper = () => (
    <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
        <GoogleLogIns/>
    </GoogleOAuthProvider>
  );
  

export default GoogleAuthProviderWrapper;

