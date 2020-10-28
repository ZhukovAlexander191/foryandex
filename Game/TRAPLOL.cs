using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TRAPLOL : MonoBehaviour
{ 
    Rigidbody2D rb;

    private void Start()
    {
        rb = GetComponent<Rigidbody2D>();
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.gameObject.name.Equals("Hero"))
        {
            rb.isKinematic = false;
        }

    }
    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.name.Equals("DEADFlor"))
        {
            Destroy(gameObject);
        }
    }

}
