import navigation from '../../configs/navigation'
import cn from 'classnames'
import styles from './style.module.css'
import { useLocation } from 'react-router-dom'
import { Button, LinkComponent } from '../index.js'

const renderMenuItem = (
  loggedIn,
  item,
  pathname
) => {
  if (!loggedIn && item.auth) { return null }
  return <li className={cn(styles['nav-menu__item'], {
      [styles['nav-menu__item_active']]: false
    })} key={item.href}>
      {pathname === item.href ? <Button
      href={item.href}
      modifier='style_dark'
      className={styles['nav-menu__button']}
    >
      {item.title}
    </Button> : <LinkComponent
      title={item.title}
      activeClassName={styles['nav-menu__link_active']}
      href={item.href}
      exact
      className={styles['nav-menu__link']}
    />}
  </li>
}

const NavMenu = ({
  loggedIn
}) => {
  const location = useLocation()
  return <ul className={styles['nav-menu']}>
    {navigation.map(item => renderMenuItem(loggedIn, item, location.pathname))}
  </ul>
}

export default NavMenu