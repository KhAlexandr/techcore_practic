```
NAME                           READY   STATUS    RESTARTS   AGE
orderworker-85445bc46d-bt9fr   1/1     Running   0          35s
orderworker-85445bc46d-ffxfj   1/1     Running   0          3h50m
orderworker-85445bc46d-hh2ct   1/1     Running   0          35s
orderworker-85445bc46d-bt9fr   1/1     Terminating   0          104s
orderworker-85445bc46d-fbgqh   0/1     Pending       0          0s
orderworker-85445bc46d-fbgqh   0/1     Pending       0          0s
orderworker-85445bc46d-bt9fr   1/1     Terminating   0          105s
orderworker-85445bc46d-fbgqh   0/1     ContainerCreating   0          1s
orderworker-85445bc46d-bt9fr   0/1     Completed           0          114s
orderworker-85445bc46d-fbgqh   1/1     Running             0          10s
orderworker-85445bc46d-bt9fr   0/1     Completed           0          115s
orderworker-85445bc46d-bt9fr   0/1     Completed           0          115s
```

```
[2025-11-05 16:25:25,572: INFO/MainProcess] celery@orderworker-85445bc46d-fbgqh ready.
[2025-11-05 16:25:26,954: INFO/MainProcess] sync with celery@orderworker-85445bc46d-ffxfj
[2025-11-05 16:25:36,461: INFO/MainProcess] sync with celery@orderworker-85445bc46d-hh2ct
[2025-11-05 16:25:27,958: INFO/MainProcess] mingle: sync with 1 nodes
[2025-11-05 16:25:27,958: INFO/MainProcess] mingle: sync complete
[2025-11-05 16:25:36,461: INFO/MainProcess] sync with celery@orderworker-85445bc46d-hh2ct
[2025-11-05 16:25:37,605: ERROR/MainProcess] Process 'ForkPoolWorker-10' pid:17 exited with 'signal 9 (SIGKILL)'
[2025-11-05 16:25:37,616: ERROR/MainProcess] Process 'ForkPoolWorker-8' pid:15 exited with 'signal 9 (SIGKILL)'
[2025-11-05 16:25:37,628: ERROR/MainProcess] Process 'ForkPoolWorker-4' pid:11 exited with 'signal 9 (SIGKILL)'
```
