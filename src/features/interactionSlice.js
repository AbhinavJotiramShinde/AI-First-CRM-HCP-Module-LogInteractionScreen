import { createSlice } from "@reduxjs/toolkit";

const interactionSlice = createSlice({
  name: "interaction",
  initialState: { form: {}, ai: {} },
  reducers: {
    setAIExtracted: (state, action) => {
      state.form = action.payload;
    }
  }
});

export const { setAIExtracted } = interactionSlice.actions;
export default interactionSlice.reducer;
