import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  name: '',
};

const filtersSlice = createSlice({
  name: "filter",
  initialState: {
    name: "",
  },
  reducers: {
    changeFilter: (state, action) => {
      return {
        ...state,
        name: action.payload,
      };
    },
  },
});

export const selectNameFilter = (state) => state.filters.name;

export const { changeFilter } = filtersSlice.actions;
export default filtersSlice.reducer;