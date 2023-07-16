import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

import { fetchWing } from './wingAPI';

/**
 * fetch wing data from API
 * @return {object}
 */
async function fetchWingFn() {
    const response = await fetchWing();
    return response.data;
}

export const fetchWingThunk = createAsyncThunk(
    'wings/fetchWing',
    fetchWingFn,
);

const wingSlice = createSlice({
    name: 'wing',
    initialState: {
        status: 'idle',
        data: null,
    },
    reducers: {
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchWingThunk.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(fetchWingThunk.fulfilled, (state, action) => {
                state.status = 'idle';
                state.data = action.payload;
            });
    },
});

export const getWing = (state) => {
    return state.wing.data;
};

export default wingSlice.reducer;
