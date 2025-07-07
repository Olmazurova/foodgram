import styles from './style.module.css'
import { Container, LinkComponent } from '../index'
import LogoFooter from '../../images/logo-footer.png'

const Footer = () => {
  return <footer className={styles.footer}>
    <Container className={styles.footer__container}>
      <LinkComponent
        href='#'
        className={styles.footer__brand}
        title={<img src={LogoFooter} className={styles.footer__logo} />}
      />

      <div className={styles['footer__menu']}>
        <ul className={styles['footer__menu-list']}>
          <li className={styles['footer__menu-item']}>
            <LinkComponent
              title='О проекте'
              href='/about'
              exact
              className={styles['footer__menu-link']}
            />
          </li>
          <li className={styles['footer__menu-item']}>
            <LinkComponent
              title='Технологии'
              href='/technologies'
              exact
              className={styles['footer__menu-link']}
            />
          </li>
        </ul>
      </div>

      <div class={styles.footer__copyright}>
      © {(new Date()).getFullYear()}
      </div>
    </Container>
  </footer>
}

export default Footer
