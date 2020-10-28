using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using UnityEngine;
using UnityEngine.UI;

public class PlayerControl : MonoBehaviour
{
    float speed = 4f;
    float move;
    public float JumpForce;
    private bool FaceR = true;

    Rigidbody2D rb;
    Animator animation;

    private bool isGrounded;
    public Transform fetPos;
    public float checkRadius;
    public LayerMask whatIsGround;
    public float health;
    private int LNumber = 10;
    public Image[] lives;
    public Sprite FullL;
    public Sprite HalfL;
    public Sprite ZeroL;
    private int p;
    private int pp;
    public GameObject panel;



    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        animation = GetComponent<Animator>();

    }

    void FixedUpdate()
    {
        rb.velocity = new Vector2(move * speed, rb.velocity.y);
        if (FaceR && move < 0)
        {
            FaceR = !FaceR;
            transform.Rotate(0f, 180f, 0f);
        }
        else if (!FaceR && move > 0)
        {
            FaceR = !FaceR;
            transform.Rotate(0f, 180f, 0f);
        }
        if (!Input.GetKeyDown(KeyCode.Space))
        {
            animation.SetInteger("Speed", Convert.ToInt32(move));
        }
    }


    private void Update()
    {
        move = Input.GetAxisRaw("Horizontal");
        isGrounded = Physics2D.OverlapCircle(fetPos.position, checkRadius, whatIsGround);
        
        if (isGrounded == true && !Input.GetKeyDown(KeyCode.Space))
        {
            animation.SetBool("jump", false);
        }
        if (isGrounded == true && Input.GetKeyDown(KeyCode.Space))
        {
            rb.velocity = Vector2.up * JumpForce;
            animation.SetBool("jump", true);
        }
        if (health <= 0)
        {
            lives[0].sprite = ZeroL;
            Destroy(gameObject);
            panel.SetActive(true);
        }
        for (int i = 0; i < health; i++)
        {
            if (i < 2)
            {
                p = 0;
                pp = 1;
            }
            else
            {
                p = i / 2;
                pp = p + 1;
            }

            if (i % 2 == 1)
            {
                lives[p].sprite = FullL;
                if ((pp < 5 && pp > 1) | health == 2) 
                {
                    lives[pp].sprite = ZeroL;
                }
            }
            else
            {
                lives[p].sprite = HalfL;
            }

            lives[p].enabled = true;

        }
    }

    public void TakeDamage(int damage)
    {
        health -= damage;
    }

}
