using System.Collections;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Security.Cryptography;
using System.Threading;
using UnityEngine;

public class EnemyMove : MonoBehaviour
{
    private float timebtwShts;
    public float startTimebtwShts;
    public int damage;

    public int health;
    public float speed;
    private float stopTime;
    public float startStopTime;
    public float normalSpeed;

    public Transform player;
    public GameObject enemyBullet;
    public Transform shotPoint;
    public float dist;
    public Transform p1;
    public Transform p2;
    bool ToRght;
    Rigidbody2D rb;

    private void Start()
    {
        player = GameObject.FindGameObjectWithTag("Player").transform;
        normalSpeed = speed;
        rb = GetComponent<Rigidbody2D>();
    }


    private void Update()
    {
        if (gameObject.transform.position.x <= p2.position.x)
        {
            ToRght = true;
        }
        if (gameObject.transform.position.x >= p1.position.x)
        {
            ToRght = false;
        }

        Destroy();
        if (Vector2.Distance(transform.position, player.position) > dist)
        {
            Moving();
        }

        if (stopTime <= 0)
        {
            speed = normalSpeed;
        }
        else
        {
            speed = 0;
            stopTime -= Time.deltaTime;
        }

        if (timebtwShts <= 0)
        {
            if (Vector2.Distance(transform.position, player.position) < dist)
            {
                if (transform.position.x > player.position.x && !ToRght)
                {
                    Instantiate(enemyBullet, shotPoint.position, transform.rotation);
                    timebtwShts = startTimebtwShts;

                }
                else if (transform.position.x > player.position.x && ToRght)
                {
                    transform.localRotation = Quaternion.Euler(0, 0, 0);
                    Instantiate(enemyBullet, shotPoint.position, transform.rotation);
                    timebtwShts = startTimebtwShts;
                    ToRght = false;
                }
                else if (transform.position.x < player.position.x && ToRght)
                {
                    Instantiate(enemyBullet, shotPoint.position, transform.rotation);
                    timebtwShts = startTimebtwShts;
                }
                else if (transform.position.x < player.position.x && !ToRght)
                {
                    transform.localRotation = Quaternion.Euler(0, 180, 0);
                    Instantiate(enemyBullet, shotPoint.position, transform.rotation);
                    timebtwShts = startTimebtwShts;
                    ToRght = true;
                }
            }
        }
        else
        {
            timebtwShts -= Time.deltaTime;
        }
    }

    public void TakeDamage(int damage)
    {
        stopTime = startStopTime;
        health -= damage;
    }

    public void Destroy()
    {
        if (health <= 0)
        {
            Destroy(gameObject);
        }
    }
    void Moving()
    {
        if (ToRght)
        {
            rb.velocity = new Vector2(speed, rb.velocity.y);
            transform.localRotation = Quaternion.Euler(0, 180, 0);
        }
        else
        {
            rb.velocity = new Vector2(-speed, rb.velocity.y);
            transform.localRotation = Quaternion.Euler(0, 0, 0);
        }
    }
}
