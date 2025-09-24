from pages.check_box_page import Checkboxpage
import time


def test_check_box(driver):
    check_box = Checkboxpage(driver)
    check_box.navigate()

    # Expand the tree
    check_box.click_expand_all()
    time.sleep(2)

    # Select the checkbox "Notes"
    check_box.click_label_notes()
    time.sleep(2)

    # Validate if checkbox was ticked
    assert check_box.check_notes_is_selected()





