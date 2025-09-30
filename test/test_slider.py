from pages.SliderPage import SliderPage
# Não precisamos mais de 'time' ou 'ActionChains', pois estamos usando a lógica de teclas

def test_slider_movement(driver):
    """
    Testa a manipulação do slider usando o método de controle por teclado,
    garantindo estabilidade e precisão.
    """
    
    # 1. Inicializa o Page Object e navega para a página
    slider_page = SliderPage(driver)
    slider_page.navigate_to_slider_page()
    assert "slider" in driver.current_url
    
    # Captura o valor inicial, que geralmente é 25
    initial_value_str = slider_page.get_current_value()
    initial_value = int(initial_value_str)
    print(f"\nValor Inicial do Slider: {initial_value}")

    # --------------------------------------------------
    # 2. AUMENTAR O SLIDER (Mover para a Direita)
    # Move 20 unidades para a direita (25 + 20 = ~45)
    move_right_units = 20
    print(f"Movendo o slider {move_right_units} unidades para a direita...")
    slider_page.move_slider_by_keys("right", move_right_units)
    
    # Captura e valida o novo valor 
    new_value_str = slider_page.get_current_value()
    new_value = int(new_value_str)
    
    # VALIDAÇÃO 1: O valor deve ter aumentado significativamente (ex: acima de 40)
    assert new_value > 40
    print(f"Novo Valor (Aumento): {new_value}. Sucesso na subida (Valor > 40).")

    # --------------------------------------------------
    # 3. DIMINUIR O SLIDER (Mover para a Esquerda)
    # Move 35 unidades para a esquerda (45 - 35 = ~10)
    move_left_units = 35 
    print(f"Movendo o slider {move_left_units} unidades para a esquerda para reduzir o valor...")
    slider_page.move_slider_by_keys("left", move_left_units)
    
    final_value_str = slider_page.get_current_value()
    final_value = int(final_value_str)

    # VALIDAÇÃO 2: O valor final DEVE ser muito baixo (ex: menor que 15), provando a redução.
    assert final_value < 15
    print(f"Valor Final (Redução): {final_value}. Sucesso na validação (Valor < 15).")
    
    print("\nTeste de Movimento do Slider concluído com sucesso.")
