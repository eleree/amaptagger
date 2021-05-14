from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re
import time

chromeDriver = webdriver.Chrome()

markCommand = "var marker = new AMap.Marker({{ position: new AMap.LngLat({:.5f}, {:.5f}),  title: '北京'}});map.add(marker);"

convertCommand = "var gps = [{:.5f}, {:.5f}];\
AMap.convertFrom(gps, 'gps', function (status, result) {{\
  if (result.info === 'ok') {{\
    var lnglats = result.locations; \
    console.log('%'+lnglats+'%');\
  }}\
}});"

# https://lbs.amap.com/api/javascript-api/summary
# https://lbs.amap.com/api/javascript-api/guide/overlays/marker#circlemarker
def queryLngLat(driver, lng, lat):
    print(markCommand.format(lng, lat))
    print(convertCommand.format(lng,lat))
    driver.get(
        "https://lbs.amap.com/demo/javascript-api/example/marker/marker-content")
    driver.implicitly_wait(20)
    driver.find_element_by_id('console_clear').click()
    #elem = driver.find_element_by_id('js_console')
    elem = driver.find_element_by_xpath(
        "//*[@id='code_console']/div/div[6]/div[1]/div/div/div/div[5]")
    elem.click()
    
    driver.implicitly_wait(10)
    ActionChains(driver).move_to_element(elem).send_keys(Keys.RETURN).perform()
    ActionChains(driver).move_to_element(elem).send_keys(convertCommand.format(lng,lat)).perform()
    ActionChains(driver).move_to_element(elem).send_keys(Keys.RETURN).perform()
    time.sleep(2)
    value = driver.find_element_by_id('output').get_attribute("innerHTML")

    convertLngLat = re.findall(r"%(.+?)%",value)[1]
    convertLng = float(convertLngLat.split(',')[0])
    convertLat = float(convertLngLat.split(',')[1])
    ActionChains(driver).move_to_element(elem).send_keys(markCommand.format(convertLng, convertLat)).perform()
    ActionChains(driver).move_to_element(elem).send_keys(Keys.RETURN).perform()
    
    time.sleep(100)


if __name__ == '__main__':
    queryLngLat(chromeDriver, 123.17778, 45.49312)
    chromeDriver.close()
