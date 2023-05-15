import React, { useEffect } from 'react'
import PropTypes from 'prop-types'
import { useLocation } from 'react-router-dom'
import { isEmpty } from 'lodash'

const REQUIRED_QUERY_PARAMS = ['id', 'first_name', 'auth_date', 'hash']

const checkForRequiredParams = (queryParams) => REQUIRED_QUERY_PARAMS.every((param) => queryParams.has(param))

const LoginViaBot = ({ handleLogin }) => {
  const location = useLocation()
  const queryParams = new URLSearchParams(location.search)

  /* eslint-disable */
  useEffect(() => {
    if (checkForRequiredParams(queryParams)) {
      const userData = {
        id: queryParams.get('id'),
        first_name: queryParams.get('first_name'),
        last_name: queryParams.get('last_name'),
        auth_date: queryParams.get('auth_date'),
        hash: queryParams.get('hash'),
        photo_url: queryParams.get('photo_url'),
        username: queryParams.get('username'),
      }
      handleLogin(userData)
    }
    else if (!isEmpty(window.Telegram.WebApp.initDataUnsafe)) {
      const userData = {
        id: window.Telegram.WebApp.initDataUnsafe.user.id,
        first_name: window.Telegram.WebApp.initDataUnsafe.user.first_name,
        last_name: window.Telegram.WebApp.initDataUnsafe.user.last_name,
        auth_date: window.Telegram.WebApp.initDataUnsafe.auth_date,
        hash: window.Telegram.WebApp.initDataUnsafe.hash,
        username: window.Telegram.WebApp.initDataUnsafe.user.username,
        init_data: window.Telegram.WebApp.initData,
      }
      handleLogin(userData)
    }
  }, [])

  /* eslint-enable */

  return (
    // eslint-disable-next-line react/no-danger
    <div dangerouslySetInnerHTML={{ __html: '<!-- Login via bot -->' }} />
  )
}

LoginViaBot.propTypes = {
  handleLogin: PropTypes.func.isRequired,
}

export default LoginViaBot