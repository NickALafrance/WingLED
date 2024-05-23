import { configureStore } from '@reduxjs/toolkit';

import counterReducer from '../features/counter/counterSlice';
import lightReducer from '../features/light/LightSlice';
import stripReducer from '../features/strip/StripSlice';
import wingReducer from '../features/wings/wingSlice';

export const store = configureStore({
    reducer: {
        counter: counterReducer,
        wing: wingReducer,
        strip: stripReducer,
        light: lightReducer,
    },
});
