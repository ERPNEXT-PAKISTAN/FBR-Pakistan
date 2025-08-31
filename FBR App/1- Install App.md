# inside your bench
---
bash```
bench new-app fbr_integration
```
# answer prompts (MIT is fine)

# install on your site
```
bench --site yoursite.local install-app fbr_integration
```
```
bench migrate && bench restart
```
