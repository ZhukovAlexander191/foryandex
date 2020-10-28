using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class STATICenemy : MonoBehaviour
{

    private float timebtwShts;
    public float startTimebtwShts;
    public int damage;

    public int health;


    public Transform player;
    public GameObject enemyBullet;
    public Transform shotPoint;
    public float dist;

    private void Start()
    {
        player = GameObject.FindGameObjectWithTag("Player").transform;
    }


    private void Update()
    {
        Destroy();
        if (timebtwShts <= 0)
        {
            if (Vector2.Distance(transform.position, player.position) < dist)
            {
                    Instantiate(enemyBullet, shotPoint.position, transform.rotation);
                    timebtwShts = startTimebtwShts;
            }
        }
        else
        {
            timebtwShts -= Time.deltaTime;
        }
    }

    public void TakeDamage(int damage)
    {
        health -= damage;
    }

    public void Destroy()
    {
        if (health <= 0)
        {
            Destroy(gameObject);
        }
    }
}
