import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import _ from 'lodash';

import { fetchLight, saveLight } from './LightAPI';

export const fetchLightAction = createAsyncThunk(
    'light/fetchLight',
    fetchLight,
);

export const saveLightAction = createAsyncThunk(
    'light/saveLight',
    saveLight,
);

const lightSlice = createSlice({
    name: 'light',
    initialState: {
        status: 'idle',
        data: {},
        selected: null,
    },
    reducers: {
        setPane(state, action) {
            state.selected = action.payload;
        },
        closePane(state) {
            state.selected = null;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchLightAction.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(fetchLightAction.fulfilled, (state, action) => {
                state.status = 'idle';
                _.set(state, `data.${action.payload.strip}.${action.payload.position}`, action.payload);
            })
            .addCase(saveLightAction.pending, (state) => {
                state.status = 'saving';
            })
            .addCase(saveLightAction.fulfilled, (state) => {
                state.status = 'idle';
                state.data = {
                    ...state.data,
                    [state.selected.strip]: {
                        ...state.data[state.selected.strip],
                        [state.selected.position]: state.selected,
                    },
                };
            });
    },
});

export const getLight = (state, stripPosition, position) => {
    return _.get(state, `light.data.${stripPosition}.${position}`, null);
};

export const getPane = (state) => {
    return state.light.selected;
};

export const isIdle = (state) => {
    return state.light.status === 'idle';
};

export const { setPane, closePane } = lightSlice.actions;

export default lightSlice.reducer;
