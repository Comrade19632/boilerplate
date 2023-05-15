import { configureStore } from '@reduxjs/toolkit'
import { isEmpty } from 'lodash'

import {AuthSlice, loginThunk} from './authSlice'

const store = configureStore({
  reducer: {
    auth: AuthSlice.reducer,
  },
})

if (!isEmpty(localStorage.getItem('accessToken')) && !isEmpty(localStorage.getItem('refreshToken'))) {
  store.dispatch(loginThunk(localStorage.getItem('accessToken'), localStorage.getItem('refreshToken')))
}

export default store