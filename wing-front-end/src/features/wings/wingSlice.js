import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

import { fetchWing } from './wingAPI';

export const fetchWingAction = createAsyncThunk(
    'wings/fetchWing',
    fetchWing,
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
            .addCase(fetchWingAction.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(fetchWingAction.fulfilled, (state, action) => {
                state.status = 'idle';
                state.data = action.payload;
            });
    },
});

export const getWing = (state) => {
    return state.wing.data;
};

export default wingSlice.reducer;
