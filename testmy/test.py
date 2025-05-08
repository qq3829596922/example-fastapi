# from datetime import datetime,timedelta
# from jose import jwt

# SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM="HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES=30 


# def create_access_token(data:dict):
#     to_encode=data.copy()
#     expire=datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp":expire})
#     print(to_encode)
#     encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
#     print(encoded_jwt)
#     return encoded_jwt

# 错误的数据将引发断言错误
# invalid_user = {"name": "李四", "age": -5}
# process_user_data(invalid_user)  # 将引发AssertionError: 年龄必须是正数
# import pytest




# print("\n--- 示例 3: 强制垃圾回收 ---")
# def example3():
#     g = demo_generator()
#     print(f"首次调用 next(): {next(g)}")
    
#     # 保存对生成器的弱引用，用于验证 GC 过程
#     import weakref
#     wr = weakref.ref(g)
    
#     print("删除生成器对象引用")
#     del g
    
#     # 强制垃圾回收
#     print("强制垃圾回收")
#     gc.collect()
    
#     print(f"弱引用是否仍有效: {wr() is not None}")

# example3()

# print("\n--- 示例 4: 完全迭代到结束 ---")
# def example4():
#     g = demo_generator()
    
#     # 迭代直到生成器自然结束
#     try:
#         while True:
#             value = next(g)
#             print(f"获得值: {value}")
#     except StopIteration as e:
#         # Python 3 中可以通过 exception 的 value 属性获取生成器的返回值
#         print(f"生成器完全迭代完毕，返回值: {e.value if e.args else None}")

# example4()

# print("\n--- 示例 5: 上下文管理器方式 ---")
# # 在 Python 3.10+ 可以直接使用 contextlib.aclosing
# from contextlib import contextmanager

# @contextmanager
# def generator_context():
#     g = demo_generator()
#     try:
#         yield g
#     finally:
#         g.close()

# def example5():
#     with generator_context() as g:
#         print(f"首次调用 next(): {next(g)}")
#         print("with 块结束会自动关闭生成器")

# example5()
# try:
#     print("aaaa")
# finally:
#     print("bbb")

numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x**2, numbers)
print(list(squared))  # [1, 4, 9, 16, 25]

