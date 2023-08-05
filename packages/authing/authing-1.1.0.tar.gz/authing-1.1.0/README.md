<h1 align="center">Welcome to authing-python-sdk 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
  <a href="https://twitter.com/fuergaosi" target="_blank">
    <img alt="Twitter: fuergaosi" src="https://img.shields.io/twitter/follow/fuergaosi.svg?style=social" />
  </a>
</p>

English | [中文](./README-zh.md)

## What is [Authing](https://authing.cn/)

Authing provides authentication and authorization as a service.

We are here to give developers and companies the building blocks they need to secure their applications without having to become security experts.

You can connect any application (written in any language or on any stack) to Authing and define the identity providers you want to use (how you want your users to log in).

Based on your app's technology, choose one of our SDKs (or call our API), and hook it up to your app. Now each time a user tries to authenticate, Authing will verify their identity and send the required information back to your app.

![https://cdn.authing.cn/github/customers/authing-pos.png](https://cdn.authing.cn/github/customers/authing-pos.png)

Develop Roadmap: [Authing Roadmap](https://github.com/Authing/authing/projects/1).

<details>
<summary><strong>What is IDaaS ?</strong></summary>

Identity as a Service (IDaaS) is a new generation of cloud computing application, which is also called Authentication as a service (AaaS) in some occasions. IDaaS is a cloud infrastructure provided by a third party to solve the problems of identity authentication and user management.

IDaaS provides secure access and data storage. When a user or an app attempts to access a protected resource, he must provide authentication information. For example, if you want to use Facebook, you must provide the account password. For example, when you vote on some wechat pages, the system will obtain your wechat personal information. In this scenario, authentication service, as a middleware, ensures that compliant users refuse illegal requests. When the authentication process is over, users can normally access the resources or application dashboard they want to access.
</details>
# Requirements

* Python 3+

# Install

```sh
pip install authing
```

# Authing SDK tutorial 🧭

## Initializing Authing
1. Use Authing UserPoolId & Secret for initialization.
You need to get `UserPoolId` and `secret`, how?,How to get t [UserPoolId & Secret](https://docs.authing.cn/authing/others/faq#ru-he-huo-qu-client-id-he-client-secret)
```py
from authing import Authing
auth = Authing({
    "userPoolId": userPoolId,
    "secret": secret,
})
```

2. Initializing with Token

```py
from authing import Authing
auth = Authing({
    "userPoolId": userPoolId,
    "token": token,
})
```

3. Initializing with Login
```python
from authing import Authing
auth = Authing({"userPoolId": userPoolId })
auth.login({
    "username": TEST_USERNAME,
    "password": TEST_PASSWORD,
})
```
## API interface
Authing-sdk implements an encapsulation of `Graphql`, so the function name and arguments correspond to the Graphql statement，[Supported Graphql Statements](./authing/graphql.py).
Take the example of querying the OIDC application information by a domain name:
The SDK's built-in Graphql statements is
```
query QueryOIDCAppInfoByDomain($domain: String){
    QueryOIDCAppInfoByDomain(domain: $domain){
        _id
        name
        domain
        image
        redirect_uris
        client_id
        client_secret
        token_endpoint_auth_method
        id_token_signed_response_alg
        id_token_encrypted_response_alg
        id_token_encrypted_response_enc
        userinfo_signed_response_alg
        userinfo_encrypted_response_alg
        userinfo_encrypted_response_enc
        request_object_signing_alg
        request_object_encryption_alg
        request_object_encryption_enc
        jwks_uri
        _jwks_uri
        custom_jwks
        jwks
        _jwks
        clientId
        grant_types
        response_types
        description
        homepageURL
        isDeleted
        isDefault
        when
        css
        authorization_code_expire
        id_token_expire
        access_token_expire
        cas_expire
        loginUrl
        customStyles{
            forceLogin
            hideQRCode
            hideUP
            hideUsername
            hideRegister
            hidePhone
            hideSocial
            hideClose
            hidePhonePassword
            defaultLoginMethod
        }
    }
}
```
So the call statement in Python SDk is
```python
res = auth.QueryOIDCAppInfoByDomain({
  domain:'test'
})
```
[View more Graphql interface information](https://docs.authing.cn/sdk/open-graphql.html)

# Example
> Register
```python
from authing import Authing
username = get_random_string(10)
password = get_random_string(10)
auth = Authing({"userPoolId": userPoolId, "secret": secret})
res = auth.register({
    "username": username,
    "password": password
})
assert res['username'] == username
```

> Show All Users
```python
from authing import Authing
auth = Authing({
    "userPoolId": userPoolId,
    "secret": secret,
})
res = auth.users()
```

> Login
```python
from authing import Authing
auth = Authing({"userPoolId": userPoolId, })
auth.login({
    "username": USERNAME,
    "password": PASSWORD,
})
print(auth.token)
```

**For more interfaces, see [Authing's Graphql documentation](https://docs.authing.cn/sdk/open-graphql.html)**


## Run **tests**

```sh
pytest
```

## Author

👤 **holegots**

* Website: https://blog.holegots.com
* Twitter: [@fuergaosi](https://twitter.com/fuergaosi)
* Github: [@fuergaosi233](https://github.com/fuergaosi233)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_