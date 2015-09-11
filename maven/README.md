# Maven Pinrepo

## Run Maven Pinrepo

The provided `nginx.conf.tmpl` contains minimum directives to make pinrepo work. Customize it to fit your own requirements; you need at least to change `MAVENREPO_CACHE_PATH, MAVENREPO_REGION, BUCKET_REGION, AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` to use your own bucket and key. Copy and overwrite your nginx server's nginx.conf and restart nginx. Be sure to copy `../nginx/proxy.conf` to your nginx config directory as well if not already. 

## Use Maven Pinrepo

To use Maven Pinrepo in your maven projects, copy the following snippet into your project's pom.xml. At minimum, you need to change the repository URL to point to your own nginx server url. 

```xml
        <repository>
            <id>pinrepo-snapshot</id>
            <name>pinrepo-snapshot</name>
            <url>http://localhost:8080/snapshot</url>
              <releases>
                <enabled>false</enabled>
              </releases>
              <snapshots>
                <enabled>true</enabled>
                <updatePolicy>always</updatePolicy>
              </snapshots>
        </repository>
        <repository>
            <id>pinrepo-release</id>
            <name>pinrepo-release</name>
            <url>http://localhost:8080/release</url>
              <releases>
                <enabled>true</enabled>
              </releases>
              <snapshots>
                <enabled>false</enabled>
              </snapshots>
        </repository>
```


## Publish Maven Artifacts

We use maven-s3-wagon plugin to publish Maven build artifacts. It's been working amazingly well for us. You can find all the details regard this maven plugin at https://github.com/jcaddel/maven-s3-wagon. 

* Copy the following snippet into your project pom.xml. Change at least the S3 URLs to point to your own bucket.

```xml
    <build>
        <extensions>  
            <extension>
                <groupId>org.kuali.maven.wagons</groupId>
                <artifactId>maven-s3-wagon</artifactId>
                <version>1.2.1</version>
            </extension>
        </extensions>
    </build>

    <distributionManagement>
        <repository>
            <id>pinrepo-release</id>
            <name>Internal Maven Release Repository</name>
            <url>s3://MAVEREPO_BUCKET/release</url>
        </repository>
        <snapshotRepository>
            <id>pinrepo-snapshot</id>
            <name>Internal Maven Snapshot Repository</name>
            <url>s3://MAVEREPO_BUCKET/snapshot</url>
        </snapshotRepository>
    </distributionManagement>
```
* Customize the following snippet and copy it to your maven profile settings.xml, usually under `${user.home}/.m2`. We separate the server profile from the project's pom.xml, so we have a better control on who and where the artifacts can be published. In practice we only make this profile available to our official build machines, so that they are the only machines could publish to pinrepo, avoid unintended and partial publications by other hosts, especially developers' hosts.

```xml
  <servers>
     <server>  
       <id>pinrepo-snapshot</id>  
       <filePermissions>Private</filePermissions>
       <username>AWS_ACCESS_KEY_ID</username>  
       <password>AWS_SECRET_ACCESS_KEY</password>
     </server>  
     <server>  
       <id>pinrepo-release</id>  
       <filePermissions>Private</filePermissions>
       <username>AWS_ACCESS_KEY_ID</username>  
       <password>AWS_SECRET_ACCESS_KEY</password>
     </server>  
  </servers>
```

* Run `mvn deploy` command will publish the build artifacts into Maven Pinrepo.
