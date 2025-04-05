import { createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

//порт
axios.defaults.baseURL = "http://localhost:8000";

export const registerUser = createAsyncThunk(
  "auth/registerUser",
  async (userData, thunkAPI) => {
    try {
      const response = await axios.post("/auth/register", userData);  
      return response.data;
    } catch (error) {
      return thunkAPI.rejectWithValue(
        error.response?.data?.detail || "Registration error"
      );
    }
  }
);

export const loginUser = createAsyncThunk(
  "auth/loginUser",
  async ({ email, password }, thunkAPI) => {
    try {
      const response = await axios.post("/auth/login", {
        username: email,  //  очікує username
        password,
      });

      const { access_token } = response.data;

      // Отримуємо по токену юзера
      const userRes = await axios.get("/users/me", {
        headers: { Authorization: `Bearer ${access_token}` },
      });

      return {
        user: userRes.data,
        token: access_token,
      };
    } catch (error) {
      return thunkAPI.rejectWithValue(
        error.response?.data?.detail || "Login error"
      );
    }
  }
);

export const verifyEmail = createAsyncThunk(
  "auth/verifyEmail",
  async (token, thunkAPI) => {
    try {
      const response = await axios.get(`/auth/verify-email?token=${token}`);
      return response.data; // { message: "Email verified" }
    } catch (error) {
      return thunkAPI.rejectWithValue(
        error.response?.data?.detail || "Email verification failed"
      );
    }
  }
);