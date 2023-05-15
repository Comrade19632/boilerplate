import React from 'react'
import { useDispatch } from 'react-redux'
import { logoutThunk } from 'redux/authSlice'
import style from './index.module.sass'

const Main = () => {
  const dispatch = useDispatch()

  const logoutOnClick = () => dispatch(logoutThunk())

  return (
    <div className={style.main}>
      Вы успешно вошли
      <button onClick={logoutOnClick} type='button'>Выйти</button>
    </div>
  )
}
export default Main
