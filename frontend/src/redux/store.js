import { configureStore } from "@reduxjs/toolkit";
import contactsReducer from "./contactsSlice";
import filtersReducer from "./filtersSlice";
import authReducer from "./auth/authSlice";
import storage from "redux-persist/lib/storage";
import persistReducer from "redux-persist/es/persistReducer";
import persistStore from "redux-persist/es/persistStore";

// Persist config
const contactsPersistConfig = {
  key: "contacts",
  storage,
  whitelist: ["items"],
};

const authPersistConfig = {
  key: "auth",
  storage,
  whitelist: ["token", "currentUser", "isVerified"],
};

// Persisted reducers
const persistedContactsReducer = persistReducer(
  contactsPersistConfig,
  contactsReducer
);
const persistedAuthReducer = persistReducer(authPersistConfig, authReducer);

// Store
export const store = configureStore({
  reducer: {
    contacts: persistedContactsReducer,
    filters: filtersReducer,
    auth: persistedAuthReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({ serializableCheck: false }),
});

export const persistor = persistStore(store);
