import styles from './styles.module.css'

const Ingredients = ({ ingredients }) => {
  if (!ingredients) { return null }
  return <div className={styles.ingredients}>
    <h3 className={styles['ingredients__title']}>Ингредиенты:</h3>
    <ul className={styles['ingredients__list']}>
      {ingredients.map(({
        name,
        amount,
        measurement_unit
      }) => <li
        key={`${name}${amount}${measurement_unit}`}
        className={styles['ingredients__list-item']}
      >
        {name} - {amount} {measurement_unit}
      </li>)}
    </ul>
  </div>
}

export default Ingredients

