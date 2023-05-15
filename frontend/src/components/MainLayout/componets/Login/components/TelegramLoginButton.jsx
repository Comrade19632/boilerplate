import React, { useRef, useEffect } from 'react'
import PropTypes from 'prop-types'

const TelegramLoginButton = ({
  botName,
  buttonSize,
  className,
  cornerRadius,
  requestAccess,
  usePic,
  dataOnauth,
  lang,
}) => {

  const instance = useRef(null)
  /* eslint-disable */
  useEffect(() => {
    if (instance) {
      window.TelegramLoginWidget = {
        dataOnauth: (user) => { dataOnauth(user) },
      }

      const script = document.createElement('script')
      script.src = 'https://telegram.org/js/telegram-widget.js?19'
      script.setAttribute('data-telegram-login', botName)
      script.setAttribute('data-size', buttonSize)
      if (cornerRadius !== undefined) {
        script.setAttribute('data-radius', cornerRadius)
      }
      script.setAttribute('data-request-access', requestAccess)
      script.setAttribute('data-userpic', usePic)
      script.setAttribute('data-lang', lang)
      script.setAttribute(
        'data-onauth',
        'TelegramLoginWidget.dataOnauth(user)',
      )
      
      script.async = true

      instance.current.appendChild(script)
    }
  }, [instance])
  
  /* eslint-enable */

  return (
    <div ref={instance} className={className} />
  )
}

TelegramLoginButton.propTypes = {
  botName: PropTypes.string,
  className: PropTypes.string,
  dataOnauth: PropTypes.func,
  buttonSize: PropTypes.oneOf(['large', 'medium', 'small']),
  cornerRadius: PropTypes.number,
  requestAccess: PropTypes.string,
  usePic: PropTypes.bool,
  lang: PropTypes.string,
}

TelegramLoginButton.defaultProps = {
  botName: 'BOILERPLATE',
  buttonSize: 'large',
  dataOnauth: () => undefined,
  lang: 'ru',
  requestAccess: 'write',
  usePic: true,
  className: null,
  cornerRadius: 10
}

export default TelegramLoginButton
