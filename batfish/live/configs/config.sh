#AS1
dynamips -P 7200 -T 2001 -A 3001 -p 1:PA-GE -p 2:PA-GE -C as1border1.cfg -X c7200-adventerprisek9-mz.153-3.XB12.image
dynamips -P 7200 -T 2001 -A 3001 -p 1:PA-GE -p 2:PA-GE -p 3:PA-GE -C as1border2.cfg -X c7200-adventerprisek9-mz.153-3.XB12.image
dynamips -P 7200 -T 2001 -A 3001 -p 1:PA-GE -p 2:PA-GE -C as1core1.cfg -X c7200-adventerprisek9-mz.153-3.XB12.image

# AS2
dynamips -P 7200 -T 2001 -A 3001 -p 1:PA-GE -p 2:PA-GE -p 3:PA-GE -C as3dist1.cfg -X c7200-adventerprisek9-mz.153-3.XB12.image
dynamips -P 7200 -T 2001 -A 3001 -p 1:PA-GE -p 2:PA-GE -p 3:PA-GE -C as3dist1.cfg -X c7200-adventerprisek9-mz.153-3.XB12.image
dynamips -P 7200 -T 2001 -A 3001 -p 1:PA-GE -p 2:PA-GE -p 3:PA-GE -C as2core1.cfg -X c7200-adventerprisek9-mz.153-3.XB12.image
dynamips -P 7200 -T 2001 -A 3001 -p 1:PA-GE -p 2:PA-GE -p 3:PA-GE -C as2core2.cfg -X c7200-adventerprisek9-mz.153-3.XB12.image

# AS3
dynamips -P 7200 -T 2001 -A 3001 -p 1:PA-GE -p 2:PA-GE -C as3border1.cfg -X c7200-adventerprisek9-mz.153-3.XB12.image
dynamips -P 7200 -T 2001 -A 3001 -p 1:PA-GE -p 2:PA-GE -p 3:PA-GE -C as3border2.cfg -X c7200-adventerprisek9-mz.153-3.XB12.image
dynamips -P 7200 -T 2001 -A 3001 -p 1:PA-GE -p 2:PA-GE -p 3:PA-GE -p 5:PA-GE -C as3core1.cfg -X c7200-adventerprisek9-mz.153-3.XB12.image
