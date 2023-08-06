通过继承线程Thread类是实现多线程

windows：
- 启动服务命令
- 杀服务命令
- adb命令
- 编码问题
```python
# 设置编码格式为rb，解决windows编码问题
    def yaml_to_dict(self) -> dict:
        with open(self.path, "rb") as f:
            yaml_file = yaml.safe_load(f)
        return yaml_file
```

使用AppiumService启动Appium
配置JDK环境，最好为JDK8

引用同一个名称的webdriver，需要用as提供别名来访问，否则容易被覆盖

解决mac上报错


理解queue里面的join和task_done方法的区别
queue中的empty方法是不可信赖的

Python中退出运行状态
```python
sys.exit(0)
```