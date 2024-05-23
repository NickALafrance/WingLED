import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import _ from 'lodash';

import { fetchStrip } from './StripAPI';

export const fetchStripAction = createAsyncThunk(
    'strip/fetchSlice',
    fetchStrip,
);

const stripSlice = createSlice({
    name: 'strip',
    initialState: {
        status: 'idle',
        data: {},
    },
    reducers: {
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchStripAction.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(fetchStripAction.fulfilled, (state, action) => {
                state.status = 'idle';
                state.data[action.payload.position] = action.payload;
            });
    },
});

export const getStrip = (state, position) => {
    return _.get(state, `strip.data.${position}`, null);
};

export default stripSlice.reducer;
