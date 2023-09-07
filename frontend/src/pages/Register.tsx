import { FormEvent, useState } from "react";

import { useNotify } from "react-admin";
import Button from "@mui/material/Button";
import Auth from "../components/Auth";
import { useNavigate } from "react-router";
import { authApi } from "../providers/env";
import { AxiosError } from "axios";
import { Link } from "react-router-dom";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const notify = useNotify();
  const navigate = useNavigate();

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    const formData = { email, password };
    try {
      const response = await authApi.registerRegister({
        userCreate: formData,
      });
      if (response.data.id) {
        notify("注册成功，您现在可以登录了", {
          type: "success",
        });
        navigate("/login");
      }
    } catch (e) {
      const exp = e as AxiosError;
      const errorMsg = exp.response?.data?.detail;
      if (errorMsg) {
        notify(errorMsg, { type: "error" });
      } else {
        notify("网络错误", { type: "error" });
      }
    }
  };

  return (
    <Auth
      setEmail={setEmail}
      setPassword={setPassword}
      actionName="Register"
      submit={submit}
      extraActions={
        <Button color="secondary" to={"/login"} component={Link}>
          Sign in
        </Button>
      }
    />
  );
};

export default Register;
