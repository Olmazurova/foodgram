import styles from './style.module.css'
import { useEffect, useState } from 'react'
import { AccountMenu, Orders, NavMenu, AccountMenuMobile, LinkComponent } from '../index.js'
import cn from 'classnames'
import { useLocation } from 'react-router-dom'
import hamburgerImg from '../../images/hamburger-menu.png'
import hamburgerImgClose from '../../images/hamburger-menu-close.png'

const Nav = ({ loggedIn, onSignOut, orders }) => {

  const [ menuToggled, setMenuToggled ] = useState(false)
  const location = useLocation()
  
  useEffect(() => {
    const cb = () => {
      setMenuToggled(false)
    }
    window.addEventListener('resize', cb)

    return () => window.removeEventListener('resize', cb)
  }, [])

  useEffect(() => {
    setMenuToggled(false)
  }, [location.pathname])

  return <div className={styles.nav}>
    <LinkComponent href="/cart" className={styles.nav__orders} title={<Orders orders={orders} />} />

    <div
      className={styles.menuButton}
      onClick={_ => setMenuToggled(!menuToggled)}
    >
      <img src={menuToggled ? hamburgerImgClose : hamburgerImg} />
    </div>
    <div className={styles.nav__container}>
      <NavMenu loggedIn={loggedIn} />
      <AccountMenu onSignOut={onSignOut} orders={orders} />
    </div>

    <div className={cn(styles['nav__container-mobile'], {
      [styles['nav__container-mobile_visible']]: menuToggled
    })}>
      <NavMenu loggedIn={loggedIn} />
      <AccountMenuMobile onSignOut={onSignOut} orders={orders} />
    </div>
  </div>
}

export default Nav
