import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'

const About = ({ updateOrders, orders }) => {
  
  return <Main>
    <MetaTags>
      <title>О проекте</title>
      <meta name="description" content="Фудграм - О проекте" />
      <meta property="og:title" content="О проекте" />
    </MetaTags>
    
    <Container>
      <h1 className={styles.title}>Привет!</h1>
      <div className={styles.content}>
        <div>
          <h2 className={styles.subtitle}>Что это за сайт?</h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
              Представляю вам проект, созданный во время обучения в Яндекс Практикуме. Этот проект — часть учебного курса, но он создан полностью самостоятельно.
            </p>
            <p className={styles.textItem}>
              Цель этого сайта — дать возможность пользователям создавать и хранить рецепты на онлайн-платформе. Кроме того, можно скачать список продуктов, необходимых для
              приготовления блюда, просмотреть рецепты друзей и добавить любимые рецепты в список избранных.
            </p>
            <p className={styles.textItem}>
              Чтобы использовать все возможности сайта — нужна регистрация. Проверка адреса электронной почты не осуществляется, вы можете ввести любой email. 
            </p>
            <p className={styles.textItem}>
              Заходите и делитесь своими любимыми рецептами!
            </p>
          </div>
        </div>
        <aside>
          <h2 className={styles.additionalTitle}>
            Ссылки
          </h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
              Код проекта находится тут - <a href="#" className={styles.textLink}>Github</a>
            </p>
            <p className={styles.textItem}>
              Автор проекта: <a href="#" className={styles.textLink}>Имя Автора</a>
            </p>
          </div>
        </aside>
      </div>
      
    </Container>
  </Main>
}

export default About

