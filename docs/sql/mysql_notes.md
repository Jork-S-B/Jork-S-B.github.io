## 📌 行行比较

```sql
--行行比较就是多个or条件的简写版
SELECT * FROM user WHERE (id, user_name)
in ((1,'u1),(2,'u3));
```

参考资料：[Mysql行行比较](https://blog.csdn.net/qq_39654841/article/details/120137935)
