import { configureStore } from "@reduxjs/toolkit";
import contactsReducer from './contactsSlice'
import filtersReducer from './filtersSlice'
import storage from "redux-persist/lib/storage";
import persistReducer from "redux-persist/es/persistReducer";
import persistStore from "redux-persist/es/persistStore";

const contactsPersistConfig = {
  key: 'contacts',
  storage,
  whitelist: ['items'], // зберігаємо лише items
};


const persistedContactsReducer = persistReducer(contactsPersistConfig, contactsReducer)


export const store = configureStore({
    reducer:{ 
      contacts: persistedContactsReducer,
      filters: filtersReducer
    },
    middleware: (getDefaultMiddleware) => getDefaultMiddleware(
      { serializableCheck: false,}
    )
  });
  
  export const persistor = persistStore(store);