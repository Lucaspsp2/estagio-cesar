import pytest
from pages.tool_tips_page import ToolTipsPage
from utils.data_loader import load_json_data

test_data = load_json_data("data/test_data.json")

@pytest.mark.widgets
def test_button_tooltip(driver):
    """Tests the tooltip on the button."""
    tool_tips_page = ToolTipsPage(driver)
    tool_tips_page.navigate(test_data["tool_tips_url"])
    
    tool_tips_page.hover_over_button()
    
    tooltip_text = tool_tips_page.get_tooltip_text()
    assert tooltip_text == test_data["tool_tip_button_text"]

@pytest.mark.widgets
def test_field_tooltip(driver):
    tool_tips_page = ToolTipsPage(driver)
    tool_tips_page.navigate(test_data["tool_tips_url"])
    
    tool_tips_page.hover_over_field()
    
    tooltip_text = tool_tips_page.get_tooltip_text()
    assert tooltip_text == test_data["tool_tip_field_text"]