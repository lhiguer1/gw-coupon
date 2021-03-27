#! /usr/bin/env python3
from selenium import webdriver
import os
import sys


if __name__ == '__main__':
    driver = webdriver.Firefox()
    driver.get('https://www.goodwillaz.org/coupons-store-specials/')
